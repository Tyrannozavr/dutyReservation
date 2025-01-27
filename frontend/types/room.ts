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
    "name": string
}

export type dateRangeType = {
    start: Date,
    end: Date
}

export interface State {
    name: string | undefined,
    duty_list: {
        name: string,
        duty_date: string,
    }[] | undefined,
    is_multiple_selection: boolean,
}