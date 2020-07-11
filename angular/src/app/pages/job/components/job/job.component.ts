import { Component, OnInit } from '@angular/core';
import { MatTabChangeEvent } from '@angular/material/tabs';
import { WebSocketService, JobInfo } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss']
})
export class JobComponent implements OnInit {

  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = { theme: 'vs-dark', language: 'python', automaticLayout: true };


  index = 0
  jobCode: string = ""

  constructor(
    public webSocketService: WebSocketService
  ) { }

  ngOnInit(): void {
  }



  sendChangedCode(job: JobInfo) {
      this.webSocketService.sendMessage({
        type: this.index == 0 && 'code' || 'vars',
        code: job.msg.code,
        vars: job.msg.vars,
        name: job.msg.name
      });
    }


  tabChanged(tabChangeEvent: MatTabChangeEvent): void {
    this.index = tabChangeEvent.index
  }

}
