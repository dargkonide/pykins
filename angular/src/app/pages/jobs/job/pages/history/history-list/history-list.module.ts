import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HistoryListRoutingModule } from './history-list-routing.module';
import { FormsModule } from '@angular/forms';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { ComponentsModule } from 'src/app/components/material.module';

import { HistoryListComponent } from './history-list.component';

@NgModule({
  declarations: [HistoryListComponent],
  imports: [
    CommonModule,
    HistoryListRoutingModule,
    ComponentsModule,
    FormsModule,
    MonacoEditorModule,
  ],
})
export class HistoryListModule {}
