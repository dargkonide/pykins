import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ComponentsModule } from 'src/app/components/material.module';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { FormsModule } from '@angular/forms';
import { JobsRoutingModule } from './jobs-history-routing.module';
import { FullCalendarModule } from '@fullcalendar/angular';

import { LogsComponent } from './logs/logs.component';
import { VarsComponent } from './vars/vars.component';
import { JobHistoryComponent } from './job-history.component';

@NgModule({
  declarations: [
    LogsComponent,
    VarsComponent,
    JobHistoryComponent,
  ],
  imports: [
    CommonModule,
    JobsRoutingModule,
    ComponentsModule,
    MonacoEditorModule,
    FullCalendarModule,
  ],
})
export class JobHistoryModule {}
