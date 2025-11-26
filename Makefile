.PHONY: help build up test logs down clean restart demo \
        logs-service1 logs-service2 logs-service3 logs-service4 \
        status benchmark large-test build-parallel up-parallel \
        down-parallel test-parallel benchmark-parallel logs-parallel \
        clean-parallel restart-parallel

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    SLEEP_CMD := timeout /t
else
    DETECTED_OS := $(shell uname -s)
    SLEEP_CMD := sleep
endif

help:
	@echo "🚀 REST/HTTP PIPELINE - Available commands:"
	@echo ""
	@echo "MAIN COMMANDS:"
	@echo "  make build    - Build all REST services"
	@echo "  make up       - Start all REST services"
	@echo "  make test     - Run REST pipeline test"
	@echo "  make logs     - Show all REST services logs"
	@echo "  make down     - Stop all REST services"
	@echo "  make clean    - Clean REST setup"
	@echo "  make restart  - Restart all REST services"
	@echo "  make demo     - Quick demo (build + up + test)"
	@echo ""
	@echo "INDIVIDUAL LOGS:"
	@echo "  make logs-service1 - Show Service 1 logs"
	@echo "  make logs-service2 - Show Service 2 logs"
	@echo "  make logs-service3 - Show Service 3 logs"
	@echo "  make logs-service4 - Show Service 4 logs"
	@echo ""
	@echo "UTILITY:"
	@echo "  make status      - Check status of REST services"
	@echo "  make benchmark   - Run performance benchmark (20 iterations)"
	@echo "  make large-test  - Run large file test"

# ==================== MAIN COMMANDS ====================

build:
	@echo "🏗️  Building REST services..."
	docker-compose build

up:
	@echo "🚀 Starting REST services..."
	docker-compose up -d \
		service1 service2 service3 service4 client
	@echo "⏳ Waiting for REST services to be ready..."
	@$(SLEEP_CMD) 10
	@echo "✅ REST SERVICES ARE RUNNING!"
	@echo ""
	@echo "🌐 SERVICE ENDPOINTS:"
	@echo "  Service 1 (Input):       http://localhost:8061"
	@echo "  Service 2 (Preprocess):  http://localhost:8062"
	@echo "  Service 3 (Analysis):    http://localhost:8063"
	@echo "  Service 4 (Report):      http://localhost:8064"
	@echo ""
	@echo "💡 Run: make test to test the system"

test:
	@echo "🧪 Running REST pipeline test..."
	docker-compose run --rm client python app.py

benchmark:
	@echo "🧪 Running benchmark test (20 iterations)..."
	docker-compose run --rm client python benchmark.py 20

large-test:
	@echo "📁 Running large file test..."
	docker-compose run --rm client python app.py

logs:
	@echo "📋 Showing all REST services logs..."
	docker-compose logs -f

logs-service1:
	@echo "📋 Showing Service 1 logs..."
	docker-compose logs -f service1

logs-service2:
	@echo "📋 Showing Service 2 logs..."
	docker-compose logs -f service2

logs-service3:
	@echo "📋 Showing Service 3 logs..."
	docker-compose logs -f service3

logs-service4:
	@echo "📋 Showing Service 4 logs..."
	docker-compose logs -f service4

down:
	@echo "🛑 Stopping REST services..."
	docker-compose down

clean: down
	@echo "🧹 Cleaning REST setup..."
	docker system prune -a --volumes --force
	@echo "✅ REST cleanup complete!"

restart: down up
	@echo "🔄 REST services restarted!"

status:
	@echo "📊 REST Services Status:"
	docker-compose ps

demo: build up test
	@echo "✅ Demo complete!"

# ==================== PARALLEL COMMANDS ====================

build-parallel:
	@echo "🏗️  Building parallel REST services..."
	docker-compose -f docker-compose-parallel.yml build

up-parallel:
	@echo "🚀 Starting parallel REST services..."
	docker-compose -f docker-compose-parallel.yml up -d \
		service1a service1b service1c service1d \
		service2a service2b service2c service2d \
		service3a service3b service3c service3d \
		service4a service4b service4c service4d \
		service1-loadbalancer service2-loadbalancer service3-loadbalancer service4-loadbalancer
	@echo "⏳ Waiting for parallel services to be ready..."
	@$(SLEEP_CMD) 15
	@echo "✅ PARALLEL SERVICES ARE RUNNING!"
	@echo ""
	@echo "🌐 LOAD BALANCERS:"
	@echo "  Service 1: localhost:8061"
	@echo "  Service 2: localhost:8062"
	@echo "  Service 3: localhost:8063"
	@echo "  Service 4: localhost:8064"
	@echo ""
	@echo "🔧 SERVICE INSTANCES:"
	@echo "  Service1: 8051, 8055, 8057, 8059"
	@echo "  Service2: 8052, 8056, 8058, 8060"
	@echo "  Service3: 8053, 8065, 8067, 8069"
	@echo "  Service4: 8054, 8066, 8068, 8070"
	@echo ""
	@echo "💡 Run: make test-parallel to test the system"

test-parallel:
	@echo "🧪 Running parallel pipeline test..."
	docker-compose -f docker-compose-parallel.yml run --rm parallel-client python app.py

benchmark-parallel:
	@echo "🧪 Running parallel benchmark test (20 iterations)..."
	docker-compose -f docker-compose-parallel.yml run --rm parallel-client python benchmark.py 20

logs-parallel:
	@echo "📋 Showing all parallel services logs..."
	docker-compose -f docker-compose-parallel.yml logs -f

down-parallel:
	@echo "🛑 Stopping parallel services..."
	docker-compose -f docker-compose-parallel.yml down

clean-parallel: down-parallel
	@echo "🧹 Cleaning parallel setup..."
	docker system prune -f
	@echo "✅ Parallel cleanup complete!"

restart-parallel: down-parallel up-parallel
	@echo "🔄 Parallel services restarted!"

.DEFAULT_GOAL := help
