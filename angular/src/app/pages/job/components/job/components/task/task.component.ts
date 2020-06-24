import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit {

  job_name: string
  // code: string = "Cacaбенза"

  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = {theme: 'vs-dark', language: 'python', automaticLayout: true};
  code: string= '';

  constructor(
    private route: ActivatedRoute,
  ) { }


  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.job_name = params['name'];
    });
  }

}
