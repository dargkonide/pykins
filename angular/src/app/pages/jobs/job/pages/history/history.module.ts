import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HistoryRoutingModule } from './history-routing.module';
import { ComponentsModule } from 'src/app/components/material.module';
import { JobsHistoryComponent } from './jobs-history/jobs-history.component';
import { JobHistoryComponent } from './job-history/job-history.component';
import { FormsModule } from '@angular/forms';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { JobsRoutingModule } from './job-history/jobs-history-routing.module';

@NgModule({
  declarations: [JobsHistoryComponent, JobHistoryComponent],
  imports: [
    CommonModule,
    HistoryRoutingModule,
    ComponentsModule,
    FormsModule,
    MonacoEditorModule,
    JobsRoutingModule,
  ],
})
export class HistoryModule {}
