// import React, { Component } from 'react'

export function DateDifference(start_date, end_date) {
  var one_day=1000*60*60*24;
  var date1_ms = (new Date(start_date)).getTime();
  var date2_ms = (new Date(end_date)).getTime();

  var difference_ms = date2_ms - date1_ms;

  return Math.round(difference_ms/one_day);
}