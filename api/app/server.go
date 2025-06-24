package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

const (
	Timeout        = 1200 * time.Millisecond
	GraphTimeout   = 2000 * time.Millisecond
	Graph3DTimeout = 2500 * time.Millisecond
)

func SetupRouter() *gin.Engine {
	router := gin.Default()

	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// Algebra
	router.POST("/evaluate", HandleOperation("evaluate_expression", Timeout))
	router.POST("/expand", HandleOperation("expand_expression", Timeout))
	router.POST("/factor", HandleOperation("factor_expression", Timeout))
	router.POST("/simplify", HandleOperation("simplify_expression", Timeout))

	// Calculus
	router.POST("/derive", HandleOperation("derive_expression", Timeout))
	router.POST("/integrate-definite", HandleOperation("integrate_definite_expression", Timeout))
	router.POST("/integrate-indefinite", HandleOperation("integrate_indefinite_expression", Timeout))
	router.POST("/limit", HandleOperation("limit_expression", Timeout))

	// Solvers
	router.POST("/solve", HandleOperation("solve_equation", Timeout))
	router.POST("/linsolve", HandleOperation("solve_linear_system", Timeout))

	// Graphs
	router.POST("/graph-func-single", HandleOperation("graph_func_single", GraphTimeout))
	router.POST("/graph-func-multiple", HandleOperation("graph_func_multiple", GraphTimeout))
	router.POST("/graph-rel-single", HandleOperation("graph_rel_single", GraphTimeout))
	router.POST("/graph-rel-multiple", HandleOperation("graph_rel_multiple", GraphTimeout))
	router.POST("/graph-parametric", HandleOperation("graph_parametric", GraphTimeout))
	router.POST("/graph-expr-single", HandleOperation("graph_expr_single", Graph3DTimeout))
	router.POST("/graph-expr-multiple", HandleOperation("graph_expr_multiple", Graph3DTimeout))

	// Misc
	router.POST("/display", HandleOperation("display_text", Timeout))

	return router
}
