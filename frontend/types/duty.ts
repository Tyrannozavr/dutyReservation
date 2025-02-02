type dutyUserType = {
    first_name: string,
    last_name: string,
    username: string,
    photo_url: string,
    link: string
}

export type dutyWithUserType = {
    id: 0,
    user: dutyUserType | null,
    date: string,
    name: string
}
export type dutyWithUserTypeList = dutyWithUserType[]

export type DutiesWithUserResponse = {
    duties: dutyWithUserTypeList
}
export type SuccessDeleteType = {
    status: "success"
}

export type groupedDutiesType = {
    date: string,
    duties: dutyWithUserTypeList
}