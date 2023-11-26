# Development Guide

## Current design Philosophy
In a very general and abstract sense, financial modeling seeks to correctly predict changes in an organization's accounting statements (output) given certain changes in the business (input).

A good model defines the relationship between those inputs and outputs reliably and efficiently. 

When *actual* business activity occurs, we record that as *actuals*. For that, no model is needed, just reporting according to the applicable accounting standards. We need a model to understand what could happen in the future, or if another set of business events had happened in the past. 

The set of future or predicted inputs to a model are *assumptions*, as they are what we assume may happen in some other version of reality. 

The last flavor of data relevant to modeling are *metrics*. These are Usually ratios of different actuals, such as revenue per sales rep or days of sales outstanding.

## Implementation

### The Account Object
The account object holds at minimum three pieces of data:
- It has an index, with at least one level holding the time or period information
- It has values which are not dependent on other data in the model for non-forecast or modeled periods
- It has a name, representable as a valid DataFrame column name

The account object is intended to be the basic level of data from which the model builds up from in the actuals period, as well as the level to which the data should output in the modeled period. However, dimensional information such as business unit or territory is not intended to be its own account. An account is the appropriate home for a *measure*, such as sales, units sold, or number of employees.
  

