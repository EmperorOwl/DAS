package main

import (
	"sync"
	"time"
)

type WorkerPool struct {
	workers     []*Worker
	mu          sync.Mutex
	next        int
	replaceChan chan int
}

func NewWorkerPool(num int) (*WorkerPool, error) {
	pool := &WorkerPool{
		replaceChan: make(chan int, num),
	}
	// Create workers
	for i := 0; i < num; i++ {
		w, err := NewWorker()
		if err != nil {
			return nil, err
		}
		pool.workers = append(pool.workers, w)
	}
	// Start async replacer
	go pool.asyncReplacer()
	// Start periodic health checker
	go pool.periodicHealthCheck()
	return pool, nil
}

// asyncReplacer listens for replacement requests and replaces dead workers
func (p *WorkerPool) asyncReplacer() {
	for idx := range p.replaceChan {
		newWorker, err := NewWorker()
		if err == nil {
			p.mu.Lock()
			p.workers[idx] = newWorker
			p.mu.Unlock()
		}
		// If err, just skip; will retry on next trigger
	}
}

// periodicHealthCheck triggers replacement for any dead workers every 30s
func (p *WorkerPool) periodicHealthCheck() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	for range ticker.C {
		p.mu.Lock()
		for i, w := range p.workers {
			if w.IsDead() {
				select {
				case p.replaceChan <- i:
				default:
				}
			}
		}
		p.mu.Unlock()
	}
}

func (p *WorkerPool) GetWorker() *Worker {
	p.mu.Lock()
	defer p.mu.Unlock()
	n := len(p.workers)
	for i := 0; i < n; i++ {
		idx := (p.next + i) % n
		w := p.workers[idx]
		if w.IsDead() {
			select {
			case p.replaceChan <- idx:
			default:
			}
			continue
		}
		if w.TryAcquire() {
			p.next = (idx + 1) % n
			return w
		}
	}
	return nil
}
