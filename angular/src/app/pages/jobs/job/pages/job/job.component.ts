import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss'],
})
export class JobComponent implements OnInit {
  links = ['code', 'vars'];

  activeLink = 'code';
  background: ThemePalette = undefined;

  constructor(public router: Router) {}

  ngOnInit(): void {}
}
