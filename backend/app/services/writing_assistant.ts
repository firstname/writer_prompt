import { AutoEventProcessor } from '../core/events/processor';
import { AutoAnalysisEngine } from '../core/analysis/engine';
import { AutoFeedbackController } from '../core/feedback/controller';
import { HealthMonitor, PerformanceMonitor } from '../core/monitoring/monitor';
import { PlotConsistencyProcessor } from '../core/analysis/processors/plot_consistency';
import { CharacterDevelopmentProcessor } from '../core/analysis/processors/character_development';
import { InlineCommentStrategy } from '../core/feedback/strategies/inline_comment';
import { StatusBarStrategy } from '../core/feedback/strategies/status_bar';

export class WritingAssistantService {
  private static instance: WritingAssistantService;
  private eventProcessor: AutoEventProcessor;
  private analysisEngine: AutoAnalysisEngine;
  private feedbackController: AutoFeedbackController;
  private healthMonitor: HealthMonitor;
  private performanceMonitor: PerformanceMonitor;

  private constructor() {
    // 初始化所有组件
    this.initializeComponents();
    // 启动监控
    this.startMonitoring();
  }

  static getInstance(): WritingAssistantService {
    if (!WritingAssistantService.instance) {
      WritingAssistantService.instance = new WritingAssistantService();
    }
    return WritingAssistantService.instance;
  }

  private initializeComponents(): void {
    // 初始化事件处理器
    this.eventProcessor = new AutoEventProcessor();

    // 初始化分析引擎
    this.analysisEngine = new AutoAnalysisEngine();
    this.initializeAnalysisProcessors();

    // 初始化反馈控制器
    this.feedbackController = new AutoFeedbackController();
    this.initializeFeedbackStrategies();

    // 初始化监控组件
    this.healthMonitor = HealthMonitor.getInstance();
    this.performanceMonitor = PerformanceMonitor.getInstance();
  }

  private initializeAnalysisProcessors(): void {
    // 注册分析处理器
    this.analysisEngine.registerProcessor(new PlotConsistencyProcessor());
    this.analysisEngine.registerProcessor(new CharacterDevelopmentProcessor());
  }

  private initializeFeedbackStrategies(): void {
    // 注册反馈策略
    this.feedbackController.addStrategy(new InlineCommentStrategy());
    this.feedbackController.addStrategy(StatusBarStrategy.getInstance());
  }

  private startMonitoring(): void {
    // 启动性能监控
    this.performanceMonitor.startMonitoring();

    // 定期检查系统健康状态
    setInterval(async () => {
      try {
        const status = await this.healthMonitor.checkHealth();
        if (!status.healthy) {
          await this.handleUnhealthyState(status);
        }
      } catch (error) {
        console.error('Health check failed:', error);
      }
    }, 60000); // 每分钟检查一次
  }

  private async handleUnhealthyState(status: any): Promise<void> {
    // 处理不健康状态
    console.error('System is unhealthy:', status);
    // TODO: 实现恢复策略
  }

  // 公共方法
  async getSystemHealth(): Promise<any> {
    return await this.healthMonitor.checkHealth();
  }

  async getPerformanceMetrics(): Promise<any> {
    // TODO: 实现获取性能指标的逻辑
    return {};
  }

  shutdown(): void {
    // 关闭所有组件
    this.eventProcessor.stop();
    this.analysisEngine.stop();
    this.feedbackController.stop();
    this.performanceMonitor.stopMonitoring();
  }
}