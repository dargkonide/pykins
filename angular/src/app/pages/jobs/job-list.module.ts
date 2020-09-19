import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { JobListRoutingModule } from './job-list-routing.module';
import { ComponentsModule } from 'src/app/components/material.module';
import { ScrollingModule } from '@angular/cdk/scrolling';

import { JobListComponent } from './job-list.component';

@NgModule({
  declarations: [JobListComponent],
  imports: [
    CommonModule,
    JobListRoutingModule,
    ComponentsModule,
    ScrollingModule
  ]
})
export class JobsListModule { }
