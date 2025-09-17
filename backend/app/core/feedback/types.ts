export enum FeedbackType {
  PLOT_ISSUE = 'plot_issue',
  CHARACTER_INCONSISTENCY = 'character_inconsistency',
  STYLE_SUGGESTION = 'style_suggestion',
  PACING_ADVICE = 'pacing_advice',
  WORLDBUILDING_TIP = 'worldbuilding_tip',
  GRAMMAR_CORRECTION = 'grammar_correction',
  CONTENT_RECOMMENDATION = 'content_recommendation',
  STRUCTURE_SUGGESTION = 'structure_suggestion'
}

export interface Feedback {
  id: string;
  type: FeedbackType;
  message: string;
  priority: number;
  context: {
    location?: {
      start: number;
      end: number;
    };
    relatedContent?: string;
    timestamp: number;
  };
  metadata: {
    source: string;
    confidence: number;
    category: string;
  };
}

export interface FeedbackResponse {
  feedbackId: string;
  action: 'accepted' | 'rejected' | 'ignored';
  timestamp: number;
  context?: any;
}

export interface FeedbackStrategy {
  type: FeedbackType;
  deliver(feedback: Feedback): Promise<void>;
  shouldDeliver(feedback: Feedback): boolean;
  getPriority(): number;
}