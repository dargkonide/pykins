import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ComponentsModule } from './components/material.module';
import { FullCalendarModule } from '@fullcalendar/angular'; // the main connector. must go first
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { HeadBarComponent } from './components/head-bar/head-bar.component';

import dayGridPlugin from '@fullcalendar/daygrid'; // a plugin
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import { LoginComponent } from './pages/login/login.component';
import { FormsModule } from '@angular/forms';

FullCalendarModule.registerPlugins([
  // register FullCalendar plugins
  dayGridPlugin,
  interactionPlugin,
  timeGridPlugin,
  listPlugin,
]);

@NgModule({
  declarations: [AppComponent, HeadBarComponent, LoginComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ComponentsModule,
    MonacoEditorModule.forRoot(),
    FullCalendarModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
