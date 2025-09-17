import { FeedbackType, Feedback, FeedbackStrategy } from '../types';

export class InlineCommentStrategy implements FeedbackStrategy {
  type = FeedbackType.PLOT_ISSUE;

  async deliver(feedback: Feedback): Promise<void> {
    // 在编辑器中显示内联注释
    await this.showInlineComment({
      text: feedback.message,
      range: feedback.context.location,
      severity: this.getSeverityLevel(feedback),
      source: feedback.metadata.source
    });
  }

  shouldDeliver(feedback: Feedback): boolean {
    return feedback.context.location !== undefined &&
           feedback.priority >= 7; // 只显示高优先级的内联注释
  }

  getPriority(): number {
    return 3;
  }

  private async showInlineComment(comment: any): Promise<void> {
    // 调用编辑器API显示内联注释
    // TODO: 实现具体的显示逻辑
  }

  private getSeverityLevel(feedback: Feedback): string {
    // 根据反馈优先级确定显示级别
    if (feedback.priority >= 9) return 'error';
    if (feedback.priority >= 7) return 'warning';
    return 'info';
  }
}