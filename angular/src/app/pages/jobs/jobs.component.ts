import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { Observable } from 'rxjs';
import { interval } from 'rxjs';

export interface IJobList{
  msg: IJob[]
}
export interface IJob{
  name: string;
  status: string;
}


@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JobsComponent implements OnInit {

  jobList$: Observable<IJobList>;

  seconds = interval(1000);

  constructor(private webSocketService: WebSocketService) {

  }

  ngOnInit(): void {
    this.jobList$ = this.webSocketService.getObservable( {type: 'jobs'} );
  }

}
