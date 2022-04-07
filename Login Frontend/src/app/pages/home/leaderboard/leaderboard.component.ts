import { Component, OnInit } from '@angular/core';
import {Notif} from '../../../model/Notif';
import {Router} from '@angular/router';
import {AuthService} from '../../../services/auth/auth.service';
import {UserService} from '../../../services/user/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MatDialog} from '@angular/material/dialog';
import {Leaderboard} from "../../../model/Leaderboard";

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.scss']
})
export class LeaderboardComponent implements OnInit {

  leaderBoard: Array<Leaderboard> = [];

  constructor(
      private router: Router,
      private authService: AuthService,
      private userService: UserService,
      private snackBar: MatSnackBar,
      public dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.userService.getLeaderboard(this.authService.currentUser.id).subscribe(response => {
      this.leaderBoard = response;
      console.log(this.leaderBoard);
    }, error => {
      this.openSnackBar(error.error.status);
    });
  }

  openSnackBar(message: string) {
    this.snackBar.open(message ? message : 'Error', null, {
      duration: 5000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
    });
  }
}
