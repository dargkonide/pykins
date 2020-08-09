import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HistoryRoutingModule } from './history-routing.module';
import { MaterialModule } from 'src/app/util/material/material.module';
import { JobsHistoryComponent } from './jobs-history/jobs-history.component';
import { JobHistoryComponent } from './job-history/job-history.component';


@NgModule({
  declarations: [JobsHistoryComponent, JobHistoryComponent],
  imports: [
    CommonModule,
    HistoryRoutingModule,
    MaterialModule
  ]
})
export class HistoryModule { }
