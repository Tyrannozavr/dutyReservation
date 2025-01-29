type dutyUser = {
    first_name: string,
    last_name: string,
    username: string,
    photo_url: string,
    link: string
}

export type dutyWithUserType = {
    id: 0,
    user: dutyUser | null,
    date: string,
    name: string
}
export type dutyWithUserTypeList = dutyWithUserType[]
export type DutiesWithUserResponse = {
    duties: dutyWithUserTypeList
}