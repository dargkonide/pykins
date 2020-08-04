import { Protocol } from 'src/app/core/services/web-socket/web-socket.service';

export interface JobList extends Protocol {
  msg: Job[];
}
export interface Job {
  name: string;
  status: string;
}

