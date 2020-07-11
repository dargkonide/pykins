import {Component, OnDestroy, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs/operators';
import { Subscription } from 'rxjs';
import { Protocol, WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';


@Component({
  selector: 'app-job-page',
  templateUrl: './job-page.component.html',
  styleUrls: ['./job-page.component.scss']
})
export class JobPageComponent implements OnInit,OnDestroy {

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
      m => this.currentJob.msg = m
    )
    this.webSocketService.currentJob$ = this.webSocketService.getObservable(this.currentJob)
  }

  ngOnDestroy(): void {
    this.currentJobSub$.unsubscribe()
  }


  changeJobName(event){
    // this.currentJob.msg = event
    // console.log("Job name changed on: ", this.currentJob.msg)
    this.webSocketService.sendMessage({type:'name',
      name:this.webSocketService.currentJob.msg.name,

    })
  }

}
