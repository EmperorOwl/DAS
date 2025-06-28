package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	// Create the worker pool before running tests
	var err error
	workerPool, err = NewWorkerPool(4)
	if err != nil {
		panic("Failed to start worker pool for tests: " + err.Error())
	}
	os.Exit(m.Run())
}

func makeTestRequest(
	t *testing.T,
	router *gin.Engine,
	method string,
	endpoint string,
	args map[string]interface{},
) (*httptest.ResponseRecorder, map[string]interface{}) {
	w := httptest.NewRecorder()
	var req *http.Request

	if method == "GET" {
		req, _ = http.NewRequest(method, endpoint, nil)
	} else {
		reqBody, _ := json.Marshal(args)
		req, _ = http.NewRequest(method, endpoint, bytes.NewBuffer(reqBody))
		req.Header.Set("Content-Type", "application/json")
	}

	router.ServeHTTP(w, req)

	var response map[string]interface{}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.Nil(t, err)

	return w, response
}

func runEndpointTest(
	t *testing.T,
	router *gin.Engine,
	method string,
	endpoint string,
	args map[string]interface{},
	expectedStatus int,
	expectedResponse map[string]interface{},
) {
	w, response := makeTestRequest(t, router, method, endpoint, args)

	assert.Equal(t, expectedStatus, w.Code)

	switch expectedStatus {
	case http.StatusOK:
		if expectedResponse != nil {
			assert.Equal(t, expectedResponse["pretty"], response["pretty"])
			if answer, exists := expectedResponse["answer"]; exists {
				assert.Equal(t, answer, response["answer"])
			}
		}
		assert.NotNil(t, response["image"])
		assert.Nil(t, response["error"])
	case http.StatusBadRequest:
		if expectedResponse != nil {
			assert.Equal(t, expectedResponse["name"], response["name"])
			assert.Equal(t, expectedResponse["message"], response["message"])
		}
	}
}

func TestHealthEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	w, response := makeTestRequest(t, router, "GET", "/health", nil)

	assert.Equal(t, 200, w.Code)
	assert.Equal(t, "ok", response["status"])
}

func TestInvalidInput(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		endpoint         string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name:           "Evaluate timeout expression",
			endpoint:       "/evaluate",
			args:           map[string]interface{}{"expr": "99^99999999!"},
			expectedStatus: http.StatusRequestEntityTooLarge,
		},
		{
			name:     "Invalid syntax",
			endpoint: "/evaluate",
			args:     map[string]interface{}{"expr": "1+"},
			expectedResponse: map[string]interface{}{
				"name":    "ParsingError",
				"message": "1+ is invalid",
			},
			expectedStatus: http.StatusBadRequest,
		},
		{
			name:     "Invalid variable name",
			endpoint: "/solve",
			args: map[string]interface{}{
				"eq":  "x+1=0",
				"var": "1",
				"dom": "real"},
			expectedResponse: map[string]interface{}{
				"name":    "ParsingError",
				"message": "1 is an invalid variable name",
			},
			expectedStatus: http.StatusBadRequest,
		},
		{
			name:     "Invalid limit value",
			endpoint: "/limit",
			args: map[string]interface{}{
				"expr": "x^2",
				"var":  "x",
				"val":  "x",
				"dir":  "+",
			},
			expectedResponse: map[string]interface{}{
				"name":    "NotImplementedError",
				"message": "Limits approaching a variable point are not supported (x -> x)",
			},
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", tc.endpoint, tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestEvaluateEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Evaluate valid expression",
			args: map[string]interface{}{"expr": "1 + 1"},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "1+1",
				},
				"answer": "2",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Evaluate trig expression",
			args: map[string]interface{}{"expr": "sin(pi/2)"},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "sin(π/2)",
				},
				"answer": "1",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/evaluate", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestExpandEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Expand valid expression",
			args: map[string]interface{}{"expr": "(x+1)^2"},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "(x+1)^2",
				},
				"answer": "x^2+2x+1",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/expand", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestFactorEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Factor valid expression",
			args: map[string]interface{}{"expr": "x^2 - 1"},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^2-1",
				},
				"answer": "(x-1)(x+1)",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/factor", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestSimplifyEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Simplify valid expression",
			args: map[string]interface{}{"expr": "sin(x)^2 + cos(x)^2"},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "sin(x)^2+cos(x)^2",
				},
				"answer": "1",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/simplify", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestDeriveEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Single variable",
			args: map[string]interface{}{
				"expr": "x^2",
				"vars": []interface{}{"x"},
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^2",
					"vars": []interface{}{"x"},
				},
				"answer": "2x",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Two variables",
			args: map[string]interface{}{
				"expr": "x^3*y^2",
				"vars": []interface{}{"x", "y"},
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^3y^2",
					"vars": []interface{}{"x", "y"},
				},
				"answer": "6x^2y",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/derive", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestIntegrateDefiniteEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Integrate definite valid expression",
			args: map[string]interface{}{
				"expr": "x^2",
				"var":  "x",
				"lt":   "0",
				"ut":   "1",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^2",
					"var":  "x",
					"lt":   "0",
					"ut":   "1",
				},
				"answer": "1/3",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/integrate-definite", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestIntegrateIndefiniteEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Integrate indefinite valid expression",
			args: map[string]interface{}{
				"expr": "x^2",
				"var":  "x",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^2",
					"var":  "x",
				},
				"answer": "x^3/3",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/integrate-indefinite", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestLimitEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Limit valid expression",
			args: map[string]interface{}{
				"expr": "x^2",
				"var":  "x",
				"val":  "0",
				"dir":  "+",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"expr": "x^2",
					"var":  "x",
					"val":  "0",
					"dir":  "+",
				},
				"answer": "0",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/limit", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestDisplayEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Display valid text",
			args: map[string]interface{}{
				"text": "Hello, world!",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"text": "Hello, world!",
				},
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/display", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestSolveEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Linear equation with one solution",
			args: map[string]interface{}{
				"eq":  "2*x - 6 = 0",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "2x-6=0",
					"var": "x",
				},
				"answer": []interface{}{"3"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Quadratic equation with two solutions",
			args: map[string]interface{}{
				"eq":  "x^2 - 4 = 0",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "x^2-4=0",
					"var": "x",
				},
				"answer": []interface{}{"-2", "2"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Quadratic equation with no solution",
			args: map[string]interface{}{
				"eq":  "x^2 + 1 = 0",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "x^2+1=0",
					"var": "x",
				},
				"answer": []interface{}{"∅"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Equation with all real numbers solution",
			args: map[string]interface{}{
				"eq":  "0 = 0",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "0=0",
					"var": "x",
				},
				"answer": []interface{}{"Reals"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Equation with all complex numbers solution",
			args: map[string]interface{}{
				"eq":  "x = x",
				"var": "x",
				"dom": "complex",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "x=x",
					"var": "x",
				},
				"answer": []interface{}{"Complexes"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Equation with closed interval solution",
			args: map[string]interface{}{
				"eq":  "x^2 <= 4",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "x^2<=4",
					"var": "x",
				},
				"answer": []interface{}{"[-2,2]"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Equation with open interval solution",
			args: map[string]interface{}{
				"eq":  "x^2 < 4",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "x^2<4",
					"var": "x",
				},
				"answer": []interface{}{"(-2,2)"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Equation with trig solution",
			args: map[string]interface{}{
				"eq":  "sin(x) = 1",
				"var": "x",
				"dom": "real",
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eq":  "sin(x)=1",
					"var": "x",
				},
				"answer": []interface{}{"2nπ+π/2"},
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/solve", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestLinsolveEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name             string
		args             map[string]interface{}
		expectedResponse map[string]interface{}
		expectedStatus   int
	}{
		{
			name: "Simple 2x2 system with unique solutions",
			args: map[string]interface{}{
				"eqs":  []interface{}{"x + y = 3", "x - y = 1"},
				"vars": []interface{}{"x", "y"},
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eqs":  []interface{}{"x+y=3", "x-y=1"},
					"vars": []interface{}{"x", "y"},
				},
				"answer": []interface{}{"2", "1"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "System with no solution",
			args: map[string]interface{}{
				"eqs":  []interface{}{"x + y = 1", "x + y = 2"},
				"vars": []interface{}{"x", "y"},
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eqs":  []interface{}{"x+y=1", "x+y=2"},
					"vars": []interface{}{"x", "y"},
				},
				"answer": []interface{}{"∅"},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "System with infinite solutions",
			args: map[string]interface{}{
				"eqs":  []interface{}{"x + y = 1", "2*x + 2*y = 2"},
				"vars": []interface{}{"x", "y"},
			},
			expectedResponse: map[string]interface{}{
				"pretty": map[string]interface{}{
					"eqs":  []interface{}{"x+y=1", "2x+2y=2"},
					"vars": []interface{}{"x", "y"},
				},
				"answer": []interface{}{"1-y", "y"},
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/linsolve", tc.args, tc.expectedStatus, tc.expectedResponse)
		})
	}
}

func TestGraphFuncSingleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Parabola",
			args: map[string]interface{}{
				"func": "x^2",
				"var":  "x",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Sine wave",
			args: map[string]interface{}{
				"func": "sin(x)",
				"var":  "x",
				"dom":  "[-1,1]",
				"ran":  "[-1,1]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph function without range",
			args: map[string]interface{}{
				"func": "sin(x)",
				"var":  "x",
				"dom":  "[-1,1]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph with modulo",
			args: map[string]interface{}{
				"func": "x + 2 % 5",
				"var":  "x",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-func-single", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphFuncMultipleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Graph two simple functions",
			args: map[string]interface{}{
				"func1": "x^2",
				"func2": "x^3",
				"var":   "x",
				"dom":   "[-5,5]",
				"ran":   "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph trigonometric functions",
			args: map[string]interface{}{
				"func1": "sin(x)",
				"func2": "cos(x)",
				"var":   "x",
				"dom":   "[-2*pi,2*pi]",
				"ran":   "[-1.5,1.5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph functions without range",
			args: map[string]interface{}{
				"func1": "x",
				"func2": "-x",
				"var":   "x",
				"dom":   "[-3,3]",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-func-multiple", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphRelSingleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Line",
			args: map[string]interface{}{
				"rel": "y = 2x",
				"dom": "[-5,5]",
				"ran": "[-10,10]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Circle",
			args: map[string]interface{}{
				"rel": "x^2 + y^2 = 1",
				"dom": "[-2,2]",
				"ran": "[-2,2]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Ellipse",
			args: map[string]interface{}{
				"rel": "x^2/4 + y^2/9 = 1",
				"dom": "[-3,3]",
				"ran": "[-4,4]",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-rel-single", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphRelMultipleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Graph circle and line",
			args: map[string]interface{}{
				"rel1": "x^2 + y^2 = 1",
				"rel2": "x + y = 0",
				"dom":  "[-2,2]",
				"ran":  "[-2,2]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph two circles",
			args: map[string]interface{}{
				"rel1": "x^2 + y^2 = 1",
				"rel2": "(x-1)^2 + y^2 = 1",
				"dom":  "[-2,3]",
				"ran":  "[-2,2]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph ellipse and hyperbola",
			args: map[string]interface{}{
				"rel1": "x^2/4 + y^2/9 = 1",
				"rel2": "x^2/4 - y^2/9 = 1",
				"dom":  "[-3,3]",
				"ran":  "[-4,4]",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-rel-multiple", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphParametricEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Graph circle parametrically",
			args: map[string]interface{}{
				"xt":      "cos(t)",
				"yt":      "sin(t)",
				"t_start": "0",
				"t_end":   "2*pi",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph ellipse parametrically",
			args: map[string]interface{}{
				"xt":      "2*cos(t)",
				"yt":      "3*sin(t)",
				"t_start": "0",
				"t_end":   "2*pi",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Graph spiral",
			args: map[string]interface{}{
				"xt":      "t*cos(t)",
				"yt":      "t*sin(t)",
				"t_start": "0",
				"t_end":   "4*pi",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-parametric", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphExprSingleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Pouch",
			args: map[string]interface{}{
				"expr": "x^2 + y^2",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Line",
			args: map[string]interface{}{
				"expr": "2x",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Flat",
			args: map[string]interface{}{
				"expr": "2",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Complex Trig",
			args: map[string]interface{}{
				"expr": "sin(xy)",
				"dom":  "[-5,5]",
				"ran":  "[-5,5]",
			},
			expectedStatus: http.StatusOK,
		},
	}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-expr-single", tc.args, tc.expectedStatus, nil)
		})
	}
}

func TestGraphExprMultipleEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := SetupRouter()

	tests := []struct {
		name           string
		args           map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Graph two 3D expressions",
			args: map[string]interface{}{
				"expr1": "x^2 + y^2",
				"expr2": "x^2 - y^2",
				"dom":   "[-2,2]",
				"ran":   "[-2,2]",
			},
			expectedStatus: http.StatusOK,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			runEndpointTest(t, router, "POST", "/graph-expr-multiple", tc.args, tc.expectedStatus, nil)
		})
	}
}
