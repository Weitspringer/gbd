import {Component, OnDestroy, OnInit} from '@angular/core';
import {GbdApiService} from './gbd/gbd-api.service';
import {Subscription} from "rxjs";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  groupsListSubs: Subscription;
  groupsList: String[];

  constructor(private groupsApi: GbdApiService) {
  }

  ngOnInit() {
    this.groupsListSubs = this.groupsApi
      .getAllGroups()
      .subscribe(res => {
          this.groupsList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.groupsListSubs.unsubscribe();
  }
}
