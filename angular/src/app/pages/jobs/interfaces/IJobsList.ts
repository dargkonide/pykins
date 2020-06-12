export interface IJobsList {
  type: string,
  message: string
  table: Array< {name: string, status: string} >
}
export interface Variable{
  name: string,
  type: string,
  description: string,
  default: any,
  input: any
}

