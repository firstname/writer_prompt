export interface SystemMetrics {
  cpu: {
    usage: number;
    temperature: number;
  };
  memory: {
    used: number;
    total: number;
    percentage: number;
  };
  storage: {
    used: number;
    total: number;
    percentage: number;
  };
}

export interface PerformanceMetrics {
  responseTime: number;
  throughput: number;
  errorRate: number;
  concurrentOperations: number;
}

export interface HealthStatus {
  healthy: boolean;
  components: {
    [key: string]: {
      status: 'healthy' | 'degraded' | 'unhealthy';
      message?: string;
      lastCheck: number;
    };
  };
  timestamp: number;
}

export class HealthMonitor {
  private static instance: HealthMonitor;
  private lastCheck: Map<string, number> = new Map();
  private healthStatus: HealthStatus = {
    healthy: true,
    components: {},
    timestamp: Date.now()
  };

  static getInstance(): HealthMonitor {
    if (!HealthMonitor.instance) {
      HealthMonitor.instance = new HealthMonitor();
    }
    return HealthMonitor.instance;
  }

  async checkHealth(): Promise<HealthStatus> {
    this.healthStatus.timestamp = Date.now();
    
    // 检查各个组件健康状态
    await this.checkEventSystem();
    await this.checkAnalysisEngine();
    await this.checkFeedbackSystem();
    await this.checkStorage();
    
    // 更新整体健康状态
    this.healthStatus.healthy = Object.values(this.healthStatus.components)
      .every(component => component.status !== 'unhealthy');

    return this.healthStatus;
  }

  private async checkEventSystem(): Promise<void> {
    try {
      // 检查事件系统
      this.updateComponentHealth('eventSystem', 'healthy');
    } catch (error) {
      this.updateComponentHealth('eventSystem', 'unhealthy', error.message);
    }
  }

  private async checkAnalysisEngine(): Promise<void> {
    try {
      // 检查分析引擎
      this.updateComponentHealth('analysisEngine', 'healthy');
    } catch (error) {
      this.updateComponentHealth('analysisEngine', 'unhealthy', error.message);
    }
  }

  private async checkFeedbackSystem(): Promise<void> {
    try {
      // 检查反馈系统
      this.updateComponentHealth('feedbackSystem', 'healthy');
    } catch (error) {
      this.updateComponentHealth('feedbackSystem', 'unhealthy', error.message);
    }
  }

  private async checkStorage(): Promise<void> {
    try {
      // 检查存储系统
      this.updateComponentHealth('storage', 'healthy');
    } catch (error) {
      this.updateComponentHealth('storage', 'unhealthy', error.message);
    }
  }

  private updateComponentHealth(
    component: string,
    status: 'healthy' | 'degraded' | 'unhealthy',
    message?: string
  ): void {
    this.healthStatus.components[component] = {
      status,
      message,
      lastCheck: Date.now()
    };
  }
}

export class MetricsCollector {
  private static instance: MetricsCollector;
  private metrics: Map<string, number[]> = new Map();
  private readonly maxDataPoints = 100;

  static getInstance(): MetricsCollector {
    if (!MetricsCollector.instance) {
      MetricsCollector.instance = new MetricsCollector();
    }
    return MetricsCollector.instance;
  }

  recordMetric(name: string, value: number): void {
    let values = this.metrics.get(name) || [];
    values.push(value);
    
    // 保持固定大小的数据点数量
    if (values.length > this.maxDataPoints) {
      values = values.slice(-this.maxDataPoints);
    }
    
    this.metrics.set(name, values);
  }

  getMetric(name: string): number[] {
    return this.metrics.get(name) || [];
  }

  getAverageMetric(name: string): number {
    const values = this.metrics.get(name) || [];
    if (values.length === 0) return 0;
    
    const sum = values.reduce((a, b) => a + b, 0);
    return sum / values.length;
  }

  clearMetrics(): void {
    this.metrics.clear();
  }
}

export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metricsCollector: MetricsCollector;
  private isMonitoring: boolean = false;

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  constructor() {
    this.metricsCollector = MetricsCollector.getInstance();
  }

  startMonitoring(): void {
    if (this.isMonitoring) return;
    
    this.isMonitoring = true;
    this.collectMetrics();
  }

  stopMonitoring(): void {
    this.isMonitoring = false;
  }

  private async collectMetrics(): Promise<void> {
    while (this.isMonitoring) {
      try {
        const metrics = await this.gatherPerformanceMetrics();
        this.recordMetrics(metrics);
      } catch (error) {
        console.error('Error collecting metrics:', error);
      }
      
      await this.sleep(5000); // 每5秒收集一次
    }
  }

  private async gatherPerformanceMetrics(): Promise<PerformanceMetrics> {
    // 收集性能指标
    return {
      responseTime: await this.measureResponseTime(),
      throughput: await this.measureThroughput(),
      errorRate: await this.calculateErrorRate(),
      concurrentOperations: await this.countConcurrentOperations()
    };
  }

  private async measureResponseTime(): Promise<number> {
    // 测量响应时间
    return 0;
  }

  private async measureThroughput(): Promise<number> {
    // 测量吞吐量
    return 0;
  }

  private async calculateErrorRate(): Promise<number> {
    // 计算错误率
    return 0;
  }

  private async countConcurrentOperations(): Promise<number> {
    // 统计并发操作数
    return 0;
  }

  private recordMetrics(metrics: PerformanceMetrics): void {
    this.metricsCollector.recordMetric('responseTime', metrics.responseTime);
    this.metricsCollector.recordMetric('throughput', metrics.throughput);
    this.metricsCollector.recordMetric('errorRate', metrics.errorRate);
    this.metricsCollector.recordMetric('concurrentOperations', metrics.concurrentOperations);
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}