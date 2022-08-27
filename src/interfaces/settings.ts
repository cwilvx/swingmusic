export enum SettingType {
  text,
  select,
  multiselect,
  switch,
}

export interface SettingOption {
  title: string;
  value: any;
}

export interface Setting {
  title: string;
  type: SettingType;
  options?: SettingOption[];
  action: (arg0?: any) => void;
  source: () => any;
}

export interface SettingGroup {
  title?: string;
  desc?: string;
  settings: Setting[];
}

export interface SettingCategory {
  title: string;
  groups: SettingGroup[];
}