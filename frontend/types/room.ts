interface RoomItem {
    id: number;
    identifier: string;
    is_multiple_selection: boolean;
    name: string;
}

export type RoomList = RoomItem[];