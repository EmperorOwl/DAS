package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

type Worker struct {
	cmd    *exec.Cmd
	stdin  io.WriteCloser
	stdout *bufio.Reader
	mu     sync.Mutex
	dead   bool
}

func NewWorker() (*Worker, error) {
	// Get the directory of the current source file
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		return nil, fmt.Errorf("could not get source file location")
	}
	currDir := filepath.Dir(filename)
	parentDir := filepath.Dir(currDir)
	scriptPath := filepath.Join(parentDir, "scripts", "worker.py")

	// Create the worker
	cmd := exec.Command("python", scriptPath)
	cmd.Env = append(os.Environ(), fmt.Sprintf("PYTHONPATH=%s", parentDir))

	stdin, err := cmd.StdinPipe()
	if err != nil {
		return nil, err
	}

	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		return nil, err
	}

	stdout := bufio.NewReader(stdoutPipe)
	if err := cmd.Start(); err != nil {
		return nil, err
	}

	return &Worker{cmd: cmd, stdin: stdin, stdout: stdout, dead: false}, nil
}

func (w *Worker) SendRequest(req interface{}, t time.Duration) ([]byte, error) {
	w.mu.Lock()
	defer w.mu.Unlock()
	if w.dead {
		return nil, fmt.Errorf("worker is dead")
	}
	data, err := json.Marshal(req)
	if err != nil {
		return nil, err
	}
	_, err = w.stdin.Write(append(data, '\n'))
	if err != nil {
		w.dead = true
		return nil, err
	}

	ch := make(chan []byte, 1)
	go func() {
		line, err := w.stdout.ReadBytes('\n')
		if err != nil {
			ch <- nil
		} else {
			ch <- line
		}
	}()

	select {
	case line := <-ch:
		if line == nil {
			w.dead = true
			return nil, fmt.Errorf("worker process died or closed pipe")
		}
		return line, nil
	case <-time.After(t):
		w.cmd.Process.Kill()
		w.dead = true
		return nil, fmt.Errorf("worker timed out and was killed")
	}
}

func (w *Worker) IsDead() bool {
	w.mu.Lock()
	defer w.mu.Unlock()
	return w.dead
}
