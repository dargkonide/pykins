import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LogsComponent } from './logs/logs.component';
import { ComponentsModule } from 'src/app/components/material.module';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { FormsModule } from '@angular/forms';
import { JobsRoutingModule } from './jobs-history-routing.module';
import { StagesComponent } from './stages/stages.component';
import { VarsComponent } from './vars/vars.component';
import { FullCalendarModule } from '@fullcalendar/angular';

@NgModule({
  declarations: [LogsComponent, StagesComponent, VarsComponent],
  imports: [
    CommonModule,
    JobsRoutingModule,
    ComponentsModule,
    FormsModule,
    MonacoEditorModule,
    FullCalendarModule,
  ],
})
export class JobHistoryModule {}
