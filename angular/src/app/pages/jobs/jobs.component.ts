import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { Observable } from 'rxjs';
import { JobList} from 'src/app/pages/jobs/interfaces/IJobsList';
import { interval } from 'rxjs';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JobsComponent implements OnInit {

  jobList$: Observable<JobList>;

  seconds = interval(1000);

  constructor(private webSocketService: WebSocketService) {

  }

  ngOnInit(): void {
    this.jobList$ = this.webSocketService.getObservable( {type: 'jobs'} );
  }

}
