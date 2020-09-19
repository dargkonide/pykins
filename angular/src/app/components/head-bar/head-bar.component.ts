import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import {DomSanitizer} from '@angular/platform-browser';


@Component({
  selector: 'app-head-bar',
  templateUrl: './head-bar.component.html',
  styleUrls: ['./head-bar.component.scss']
})
export class HeadBarComponent implements OnInit {

  constructor(private matIconRegistry: MatIconRegistry,
              private domSanitizer: DomSanitizer){
    this.matIconRegistry.addSvgIcon(
      'python',
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/python.svg')
    );
  }

  ngOnInit(): void {
  }

}
