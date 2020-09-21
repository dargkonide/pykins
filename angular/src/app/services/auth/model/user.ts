import { Role } from "./role";
import {Protocol} from "../../web-socket/web-socket.service"

export interface IAuth extends Protocol{
    msg?: IUser
}
export interface IUser {
    id: number;
    firstName?: string;
    lastName?: string;
    username: string;
    role: Role;
    token?: string;
}