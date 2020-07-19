import { Component, OnInit, OnDestroy } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { MatTabChangeEvent } from '@angular/material/tabs';
import { WebSocketService, JobInfo } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../service/job.service';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss']
})
export class JobComponent implements OnInit {

  links = ['code', 'vars'];
  // TODO: Вставить активный линк из роута
  // Еще бы и вкладку запоминала, а?
  activeLink = this.links[0];
  background: ThemePalette = undefined;

  constructor(

  ) { }

  ngOnInit(): void {
  }

  

}
