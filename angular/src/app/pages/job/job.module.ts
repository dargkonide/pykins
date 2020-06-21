import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobRoutingModule } from './job-routing.module';
import { JobPageComponent } from './job-page.component';
import { HistoryComponent } from './components/history/history.component';
import { BuildComponent } from './components/build/build.component';
import { JobComponent } from './components/job/job.component';
import { MaterialModule } from 'src/app/util/material/material.module';


@NgModule({
  declarations: [JobPageComponent, JobComponent, HistoryComponent, BuildComponent],
  imports: [
    CommonModule,
    JobRoutingModule,
    MaterialModule
  ]
})
export class JobModule { }
