import { Component, OnInit } from '@angular/core';
import { WebSocketService, JobInfo } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit {

  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = {theme: 'vs-dark', language: 'python', automaticLayout: true};

  constructor(
    public webSocketService: WebSocketService
  ) {
   }

  ngOnInit(): void {
  }

  ngOnDestory(): void {
  }

  sendChangedCode(){

  }

}
