package main

import (
	"sync"
)

type WorkerPool struct {
	workers []*Worker
	mu      sync.Mutex
	next    int
}

func NewWorkerPool(num int) (*WorkerPool, error) {
	pool := &WorkerPool{}
	for i := 0; i < num; i++ {
		w, err := NewWorker()
		if err != nil {
			return nil, err
		}
		pool.workers = append(pool.workers, w)
	}
	return pool, nil
}

func (p *WorkerPool) GetWorker() *Worker {
	p.mu.Lock()
	defer p.mu.Unlock()
	for i := 0; i < len(p.workers); i++ {
		w := p.workers[p.next]
		if w.IsDead() {
			// Replace dead worker
			newWorker, err := NewWorker()
			if err == nil {
				p.workers[p.next] = newWorker
				p.next = (p.next + 1) % len(p.workers)
				return newWorker
			}
			// If replacement fails, skip this worker
			p.next = (p.next + 1) % len(p.workers)
			continue
		}
		p.next = (p.next + 1) % len(p.workers)
		return w
	}
	return nil // All workers dead and replacement failed
}
