import {Component, OnDestroy, OnInit} from '@angular/core';
import { WebSocketService, JobInfo } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit,OnDestroy{

  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = {theme: 'vs-dark', language: 'python', automaticLayout: true};

  constructor(
    public webSocketService: WebSocketService
  ) {
   }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
  }

  sendChangedCode(){
    this.webSocketService.sendMessage({type:'code',
      code:this.webSocketService.currentJob.msg.code,
      name:this.webSocketService.currentJob.msg.name});
    // console.log("Save changes",code)
  }

}
