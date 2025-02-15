interface RoomItem {
    id: number;
    identifier: string;
    is_multiple_selection: boolean;
    name: string;
}

export type RoomList = RoomItem[];

export type RoomRead = {
    "identifier": string,
    "is_multiple_selection": boolean,
    "name": string | null
}
export type RoomReadList = RoomRead[]

export type RoomOwnerRead = {
    "id": number,
    "identifier": string,
    "is_multiple_selection": boolean,
    "name": string
}
export type RoomOwnerReadList = RoomOwnerRead[]

export type dateRangeType = {
    start: Date,
    end: Date
}
export type dutyType = {
    name: string,
    duty_date: string,
}

export type dutyListType = dutyType[]

export interface State {
    name: string | undefined,
    duty_list: dutyListType | undefined,
    is_multiple_selection: boolean,
}

