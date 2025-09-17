import { WritingEvent, WritingEventType, Priority } from './types';

interface EventListener {
  handle(event: WritingEvent): Promise<void>;
}

class PriorityQueue<T> {
  private items: { item: T; priority: number }[] = [];

  enqueue(item: T, priority: number): void {
    const queueItem = { item, priority };
    let added = false;

    for (let i = 0; i < this.items.length; i++) {
      if (this.items[i].priority > priority) {
        this.items.splice(i, 0, queueItem);
        added = true;
        break;
      }
    }

    if (!added) {
      this.items.push(queueItem);
    }
  }

  dequeue(): T | undefined {
    const item = this.items.shift();
    return item?.item;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }
}

interface ContentChange {
  documentId: string;
  content: string;
  position: {
    line: number;
    character: number;
  };
  timestamp: number;
}

class ContentObserver {
  private callback: ((change: ContentChange) => void) | null = null;
  private debounceTimeout: NodeJS.Timeout | null = null;
  private changes: ContentChange[] = [];

  startObserving(callback: (change: ContentChange) => void): void {
    this.callback = callback;
    this.setupDocumentListeners();
  }

  private setupDocumentListeners(): void {
    // 设置编辑器文档更改监听
    // 这里需要根据实际使用的编辑器实现具体的监听逻辑
  }

  private handleChange(change: ContentChange): void {
    this.changes.push(change);
    
    if (this.debounceTimeout) {
      clearTimeout(this.debounceTimeout);
    }

    this.debounceTimeout = setTimeout(() => {
      this.processChanges();
    }, 500);
  }

  private processChanges(): void {
    if (!this.callback || this.changes.length === 0) return;

    const mergedChange = this.mergeChanges(this.changes);
    this.callback(mergedChange);
    this.changes = [];
  }

  private mergeChanges(changes: ContentChange[]): ContentChange {
    // 合并短时间内的多个更改
    return changes[changes.length - 1]; // 简化处理，实际应该更智能地合并
  }
}

export class AutoEventProcessor {
  private listeners: Map<WritingEventType, EventListener[]> = new Map();
  private queue: PriorityQueue<WritingEvent> = new PriorityQueue();
  private contentObserver: ContentObserver;
  private isProcessing: boolean = false;

  constructor() {
    this.contentObserver = new ContentObserver();
    this.initializeContentObserver();
    this.startBackgroundProcessing();
  }

  private initializeContentObserver(): void {
    this.contentObserver.startObserving((change) => {
      this.handleContentChange(change);
    });
  }

  private async startBackgroundProcessing(): Promise<void> {
    this.isProcessing = true;
    while (this.isProcessing) {
      await this.processQueue();
      await this.sleep(100);
    }
  }

  private async handleContentChange(change: ContentChange): Promise<void> {
    const event = this.createEventFromChange(change);
    this.queue.enqueue(event, event.priority);
  }

  private async processQueue(): Promise<void> {
    while (!this.queue.isEmpty()) {
      const event = this.queue.dequeue();
      if (!event) continue;

      const listeners = this.listeners.get(event.type) || [];
      await Promise.all(listeners.map(listener => listener.handle(event)));
    }
  }

  private createEventFromChange(change: ContentChange): WritingEvent {
    return {
      id: crypto.randomUUID(),
      type: this.determineEventType(change),
      content: change.content,
      timestamp: Date.now(),
      priority: this.calculatePriority(change),
      context: this.extractContext(change)
    };
  }

  private determineEventType(change: ContentChange): WritingEventType {
    // 根据内容变化判断事件类型
    // 这里需要实现智能判断逻辑
    return WritingEventType.CONTENT_CHANGE;
  }

  private calculatePriority(change: ContentChange): Priority {
    // 根据变化内容和上下文计算优先级
    return Priority.MEDIUM;
  }

  private extractContext(change: ContentChange): WritingContext {
    // 提取上下文信息
    return {
      documentId: change.documentId,
      position: change.position,
      surrounding: {
        before: '', // 需要从文档中获取
        after: ''  // 需要从文档中获取
      },
      metadata: {
        timestamp: change.timestamp
      }
    };
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 公共方法
  addListener(type: WritingEventType, listener: EventListener): void {
    const listeners = this.listeners.get(type) || [];
    listeners.push(listener);
    this.listeners.set(type, listeners);
  }

  removeListener(type: WritingEventType, listener: EventListener): void {
    const listeners = this.listeners.get(type) || [];
    const index = listeners.indexOf(listener);
    if (index !== -1) {
      listeners.splice(index, 1);
      this.listeners.set(type, listeners);
    }
  }

  stop(): void {
    this.isProcessing = false;
  }
}