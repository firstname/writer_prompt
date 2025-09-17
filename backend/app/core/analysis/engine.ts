import { AnalysisType, AnalysisTask, AnalysisResult, ContentProcessor } from './types';

class AnalysisScheduler {
  private scheduledTasks: Map<string, AnalysisTask> = new Map();
  private processingTasks: Set<string> = new Set();
  private lastAnalysisTime: Map<AnalysisType, number> = new Map();
  private analysisIntervals: Map<AnalysisType, number> = new Map();

  constructor() {
    this.initializeIntervals();
  }

  private initializeIntervals(): void {
    // 设置不同类型分析的默认间隔时间（毫秒）
    this.analysisIntervals.set(AnalysisType.PLOT_CONSISTENCY, 300000);  // 5分钟
    this.analysisIntervals.set(AnalysisType.CHARACTER_DEVELOPMENT, 600000);  // 10分钟
    this.analysisIntervals.set(AnalysisType.WORLD_BUILDING, 900000);  // 15分钟
    this.analysisIntervals.set(AnalysisType.WRITING_STYLE, 60000);  // 1分钟
    this.analysisIntervals.set(AnalysisType.PACING, 300000);  // 5分钟
    this.analysisIntervals.set(AnalysisType.DIALOGUE, 120000);  // 2分钟
    this.analysisIntervals.set(AnalysisType.THEME, 1800000);  // 30分钟
    this.analysisIntervals.set(AnalysisType.STRUCTURE, 600000);  // 10分钟
  }

  scheduleAnalysis(task: AnalysisTask): void {
    // 检查是否需要调度新的分析任务
    if (this.shouldScheduleAnalysis(task)) {
      this.scheduledTasks.set(task.id, task);
    }
  }

  private shouldScheduleAnalysis(task: AnalysisTask): boolean {
    const lastTime = this.lastAnalysisTime.get(task.type) || 0;
    const interval = this.analysisIntervals.get(task.type) || 300000; // 默认5分钟
    
    return Date.now() - lastTime >= interval;
  }

  getPendingTasks(): AnalysisTask[] {
    const now = Date.now();
    const pendingTasks: AnalysisTask[] = [];

    for (const [id, task] of this.scheduledTasks) {
      if (!this.processingTasks.has(id)) {
        const interval = this.analysisIntervals.get(task.type) || 300000;
        const lastTime = this.lastAnalysisTime.get(task.type) || 0;

        if (now - lastTime >= interval) {
          pendingTasks.push(task);
          this.processingTasks.add(id);
        }
      }
    }

    return pendingTasks.sort((a, b) => a.priority - b.priority);
  }

  markTaskComplete(taskId: string, type: AnalysisType): void {
    this.scheduledTasks.delete(taskId);
    this.processingTasks.delete(taskId);
    this.lastAnalysisTime.set(type, Date.now());
  }

  adjustInterval(type: AnalysisType, processingTime: number, resultQuality: number): void {
    const currentInterval = this.analysisIntervals.get(type) || 300000;
    let newInterval = currentInterval;

    // 根据处理时间和结果质量动态调整间隔
    if (processingTime > 5000 || resultQuality < 0.7) {
      newInterval = Math.min(currentInterval * 1.2, 3600000); // 最大1小时
    } else if (processingTime < 1000 && resultQuality > 0.9) {
      newInterval = Math.max(currentInterval * 0.8, 30000); // 最小30秒
    }

    this.analysisIntervals.set(type, newInterval);
  }

  getOptimalInterval(): number {
    // 返回所有分析类型中最小的间隔时间
    return Math.min(...Array.from(this.analysisIntervals.values()));
  }
}

class ContentWatcher {
  private content: string = '';
  private changeListeners: ((change: any) => void)[] = [];
  private idleListeners: (() => void)[] = [];
  private idleTimeout: any = null;
  private isIdle: boolean = true;

  constructor() {
    this.setupChangeDetection();
  }

  private setupChangeDetection(): void {
    // 监听文档变化的实现
    // 需要根据实际编辑器环境来实现
  }

  onContentChange(listener: (change: any) => void): void {
    this.changeListeners.push(listener);
  }

  onIdle(listener: () => void): void {
    this.idleListeners.push(listener);
  }

  private handleContentChange(newContent: string): void {
    this.content = newContent;
    this.isIdle = false;

    // 清除之前的空闲超时
    if (this.idleTimeout) {
      clearTimeout(this.idleTimeout);
    }

    // 通知所有变化监听器
    this.changeListeners.forEach(listener => listener({
      content: newContent,
      timestamp: Date.now()
    }));

    // 设置新的空闲超时
    this.idleTimeout = setTimeout(() => {
      this.isIdle = true;
      this.idleListeners.forEach(listener => listener());
    }, 3000); // 3秒无变化判定为空闲
  }

  async getFullContent(): Promise<string> {
    return this.content;
  }
}

export class AutoAnalysisEngine {
  private processors: Map<AnalysisType, ContentProcessor> = new Map();
  private scheduler: AnalysisScheduler;
  private contentWatcher: ContentWatcher;
  private running: boolean = false;

  constructor() {
    this.scheduler = new AnalysisScheduler();
    this.contentWatcher = new ContentWatcher();
    this.initializeProcessors();
    this.setupContentWatcher();
    this.startAutomaticAnalysis();
  }

  private initializeProcessors(): void {
    // 初始化各种内容处理器
    // 需要实现具体的处理器类
  }

  private setupContentWatcher(): void {
    this.contentWatcher.onContentChange(async (change) => {
      await this.handleContentChange(change);
    });

    this.contentWatcher.onIdle(async () => {
      await this.performDeepAnalysis();
    });
  }

  private async startAutomaticAnalysis(): Promise<void> {
    this.running = true;
    while (this.running) {
      await this.runScheduledAnalysis();
      await this.optimizeProcessors();
      await this.sleep(this.scheduler.getOptimalInterval());
    }
  }

  private async handleContentChange(change: any): Promise<void> {
    const task: AnalysisTask = {
      id: crypto.randomUUID(),
      type: this.determineAnalysisType(change),
      content: change.content,
      priority: this.calculatePriority(change),
      context: change,
      timestamp: Date.now()
    };

    this.scheduler.scheduleAnalysis(task);
  }

  private determineAnalysisType(change: any): AnalysisType {
    // 根据变化内容确定最适合的分析类型
    // 需要实现智能判断逻辑
    return AnalysisType.WRITING_STYLE;
  }

  private calculatePriority(change: any): number {
    // 根据变化内容计算优先级
    return 1;
  }

  private async runScheduledAnalysis(): Promise<void> {
    const tasks = this.scheduler.getPendingTasks();
    
    for (const task of tasks) {
      const processor = this.processors.get(task.type);
      if (processor && processor.canProcess(task.content)) {
        try {
          const startTime = Date.now();
          const result = await processor.process(task.content);
          const processingTime = Date.now() - startTime;

          this.scheduler.adjustInterval(
            task.type,
            processingTime,
            result.metadata.confidence
          );

          await this.handleAnalysisResult(result);
          this.scheduler.markTaskComplete(task.id, task.type);
        } catch (error) {
          console.error(`Error processing task ${task.id}:`, error);
        }
      }
    }
  }

  private async performDeepAnalysis(): Promise<void> {
    const content = await this.contentWatcher.getFullContent();
    
    // 执行深度分析
    const analysisTypes = [
      AnalysisType.PLOT_CONSISTENCY,
      AnalysisType.CHARACTER_DEVELOPMENT,
      AnalysisType.WORLD_BUILDING
    ];

    for (const type of analysisTypes) {
      const processor = this.processors.get(type);
      if (processor && processor.canProcess(content)) {
        try {
          const result = await processor.process(content);
          await this.handleAnalysisResult(result);
        } catch (error) {
          console.error(`Error in deep analysis for ${type}:`, error);
        }
      }
    }
  }

  private async handleAnalysisResult(result: AnalysisResult): Promise<void> {
    // 处理分析结果
    // 可能需要触发事件或更新UI等
  }

  private async optimizeProcessors(): Promise<void> {
    // 优化处理器性能和资源使用
    // 可能包括缓存清理、资源释放等
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 公共方法
  stop(): void {
    this.running = false;
  }

  registerProcessor(processor: ContentProcessor): void {
    this.processors.set(processor.type, processor);
  }
}