import { Component, OnInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { Observable, Subscription, throwError } from 'rxjs';
import { IJobsList, IRows } from 'src/app/pages/jobs/interfaces/IJobsList';
import { MatTableDataSource } from '@angular/material/table';
import { interval } from 'rxjs';
import { map, timeout, timeoutWith, catchError } from 'rxjs/operators';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JobsComponent implements OnInit {

  jobList$: Observable<IJobsList>
  jobListSubs: Subscription
  jobList: IRows[] = []

  seconds = interval(1000);

  constructor(private webSocketService: WebSocketService) {
    this.jobList$ = this.webSocketService.getObservable("jobList").pipe(
      timeout(500),
      catchError(
        (err?) => {
          return throwError("Timeout has occurred" + err);
        }
      ),

    );
  }

  ngOnInit(): void {
    // this.jobListSubs = this.jobList$.subscribe(
    //   (message?: IJobsList) => {
    //     this.jobList.push(...message.table);
    //     console.log(this.jobList);
    //   }
    // )
  }

  ngOnDestroy(): void {
    // this.jobListSubs.unsubscribe();
  }

}
