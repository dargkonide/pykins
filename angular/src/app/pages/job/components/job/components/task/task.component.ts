import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit {

  job_name: string
  code: string = "Cacaбенза"

  constructor(
    private route: ActivatedRoute,
  ) { }


  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.job_name = params['name'];
    });
  }

}
