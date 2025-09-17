export enum WritingEventType {
  CONTENT_CHANGE = 'content_change',
  SECTION_COMPLETE = 'section_complete',
  CHARACTER_MENTION = 'character_mention',
  PLOT_POINT = 'plot_point',
  WORLD_BUILDING = 'world_building',
  STYLE_CHANGE = 'style_change',
  CONSISTENCY_CHECK = 'consistency_check',
  ANALYSIS_COMPLETE = 'analysis_complete',
  FEEDBACK_READY = 'feedback_ready'
}

export enum Priority {
  CRITICAL = 0,
  HIGH = 1,
  MEDIUM = 2,
  LOW = 3,
  BACKGROUND = 4
}

export interface WritingContext {
  documentId: string;
  sectionId?: string;
  position: {
    line: number;
    character: number;
  };
  surrounding: {
    before: string;
    after: string;
  };
  metadata: {
    characters?: string[];
    locations?: string[];
    plotPoints?: string[];
    timestamp: number;
  };
}

export interface WritingEvent {
  id: string;
  type: WritingEventType;
  content: any;
  timestamp: number;
  priority: Priority;
  context: WritingContext;
}