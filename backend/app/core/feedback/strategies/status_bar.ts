import { FeedbackType, Feedback, FeedbackStrategy } from '../types';

export class StatusBarStrategy implements FeedbackStrategy {
  type = FeedbackType.STYLE_SUGGESTION;
  private static instance: StatusBarStrategy;
  private currentNotification: any = null;

  static getInstance(): StatusBarStrategy {
    if (!StatusBarStrategy.instance) {
      StatusBarStrategy.instance = new StatusBarStrategy();
    }
    return StatusBarStrategy.instance;
  }

  async deliver(feedback: Feedback): Promise<void> {
    // 在状态栏显示通知
    if (this.currentNotification) {
      await this.clearCurrentNotification();
    }

    this.currentNotification = await this.showStatusBarNotification({
      text: this.formatMessage(feedback),
      type: this.getNotificationType(feedback),
      duration: this.calculateDuration(feedback)
    });
  }

  shouldDeliver(feedback: Feedback): boolean {
    return feedback.priority <= 5 && // 低优先级的反馈
           !feedback.context.location; // 不需要指定位置的反馈
  }

  getPriority(): number {
    return 1;
  }

  private async showStatusBarNotification(notification: any): Promise<any> {
    // 调用编辑器API显示状态栏通知
    // TODO: 实现具体的显示逻辑
    return null;
  }

  private async clearCurrentNotification(): Promise<void> {
    if (this.currentNotification) {
      // 清除当前通知
      // TODO: 实现具体的清除逻辑
      this.currentNotification = null;
    }
  }

  private formatMessage(feedback: Feedback): string {
    // 格式化消息以适合状态栏显示
    return feedback.message.length > 50 
      ? feedback.message.substring(0, 47) + '...'
      : feedback.message;
  }

  private getNotificationType(feedback: Feedback): string {
    // 根据反馈类型确定通知类型
    return 'info';
  }

  private calculateDuration(feedback: Feedback): number {
    // 计算通知显示时长（毫秒）
    return 5000; // 默认5秒
  }
}