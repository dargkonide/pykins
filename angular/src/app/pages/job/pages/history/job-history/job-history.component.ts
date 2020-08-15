import { Component, OnInit } from '@angular/core';
import {ThemePalette} from '@angular/material/core';

@Component({
  selector: 'app-job-history',
  templateUrl: './job-history.component.html',
  styleUrls: ['./job-history.component.scss']
})
export class JobHistoryComponent implements OnInit {
  links = ['logs', 'vars', 'stages'];
  activeLink = 'logs';
  background: ThemePalette = undefined;

  constructor() { }

  ngOnInit(): void {
  }

}
