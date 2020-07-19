import {Component, OnDestroy, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';
import { Subscription } from 'rxjs';
import { Protocol, WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobComponent } from './components/job/job.component';


@Component({
  selector: 'app-job-page',
  templateUrl: './job-page.component.html',
  styleUrls: ['./job-page.component.scss']
})
export class JobPageComponent implements OnInit,OnDestroy {

  jobRoute: string
  currentJob: Protocol = {type:"job"}
  currentJobSub$: Subscription

  constructor(
    private route: ActivatedRoute,
    private webSocketService: WebSocketService
  ) {

  }

  ngOnInit(): void {
    this.currentJobSub$ = this.route.params.pipe(map(p => p.name))
    .subscribe(
      m => {
        this.currentJob.msg = m
        this.jobRoute = m
      }
    )
    this.updateJobObservable()
  }

  updateJobObservable(){
    this.webSocketService.currentJob$ = this.webSocketService.getObservable(this.currentJob)
    // this.jobPage.updateJob()
  }

  ngOnDestroy(): void {
    this.currentJobSub$.unsubscribe()
  }


  changeJobName(event){
    this.webSocketService.sendMessage({
      type:'name',
      new:this.currentJob.msg,
      old:this.jobRoute
    })
    this.updateJobObservable()
  }
    
    

}
