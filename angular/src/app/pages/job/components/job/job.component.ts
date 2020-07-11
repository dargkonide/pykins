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
  code
  vars
  jobName

  constructor(
    public webSocketService: WebSocketService
  ) { }

  ngOnInit(): void {
    this.webSocketService.currentJob$.subscribe(
      m => {
        this.code = m.msg.code
        this.vars = m.msg.vars
        this.jobName = m.msg.name

        this.jobCode = this.index == 0 && this.code || this.vars
      }
    )
  }

  sendChangedCode() {
    if (this.index == 0) this.code = this.jobCode
    else this.vars = this.jobCode

    this.webSocketService.sendMessage({
      type: this.index == 0 && 'code' || 'vars',
      code: this.code,
      vars: this.vars,
      name: this.jobName
    });
  }

  tabChanged(tabChangeEvent: MatTabChangeEvent): void {
    this.index = tabChangeEvent.index
    this.jobCode = this.index == 0 && this.code || this.vars
    console.log(this.index)
  }

}
