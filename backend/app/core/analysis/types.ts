export enum AnalysisType {
  PLOT_CONSISTENCY = 'plot_consistency',
  CHARACTER_DEVELOPMENT = 'character_development',
  WORLD_BUILDING = 'world_building',
  WRITING_STYLE = 'writing_style',
  PACING = 'pacing',
  DIALOGUE = 'dialogue',
  THEME = 'theme',
  STRUCTURE = 'structure'
}

export interface AnalysisTask {
  id: string;
  type: AnalysisType;
  content: string;
  priority: number;
  context?: any;
  timestamp: number;
}

export interface AnalysisResult {
  taskId: string;
  type: AnalysisType;
  findings: Array<{
    type: string;
    severity: 'critical' | 'warning' | 'suggestion';
    message: string;
    location?: {
      start: number;
      end: number;
    };
    context?: any;
  }>;
  metadata: {
    processingTime: number;
    confidence: number;
    timestamp: number;
  };
}

export interface ContentProcessor {
  type: AnalysisType;
  process(content: string): Promise<AnalysisResult>;
  canProcess(content: string): boolean;
  getPriority(): number;
}