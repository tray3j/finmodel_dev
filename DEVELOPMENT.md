# Development Guide

## Current design Philosophy
In a very general and abstract sense, financial modeling seeks to correctly predict changes in an organization's accounting statements (output) given certain changes in the business (input).

A good model defines the relationship between those inputs and outputs reliably and efficiently. 

When *actual* business activity occurs, we record that as *actuals*. For that, no model is needed, just reporting according to the applicable accounting standards. We need a model to understand what could happen in the future, or if another set of business events had happened in the past. 

The set of future or predicted inputs to a model are *assumptions*, as they are what we assume may happen in some other version of reality. 

The last flavor of data relevant to modeling are *metrics*. These are Usually ratios of different actuals, such as revenue per sales rep or days of sales outstanding.

## Motivation

This project is built because in our experience, corporate finance demands can become complicated enough to merit a more robust tool than excel, even though we consider excel to be a fantastic tool for many uses. The benefits of a tool such as finmodel include:

- Clear separation of logic from assumptions to enable robust sensitivity and simulation capabilities
- Native time period handling
- Supports significantly larger data input sizes (slows down only at the gigabyte level instead of megabytes)
- Ability to implement much more scalable testing and correctness checking
- nearly limitless customizability of logic and data input

## Implementation

### The modeling cycle
The life cycle of a model is assumed to be:
- Actuals are generated by a data generating process
- Metrics are calculated based upon those actuals, in sequence
- Assumptions are made about the modeled state of actuals and/or metrics 
- The modeled values are calculated at the same level of detail as the Actuals





### The Account Object
The account object holds at minimum three pieces of data:
- It has an index, with at least one level holding the time or period information
- It has values which are not dependent on other data in the model for non-forecast or modeled periods
- It has a name, representable as a valid DataFrame column name

The account object is intended to be the basic level of data from which the model builds up from in the actuals period, as well as the level to which the data should output in the modeled period. However, dimensional information such as business unit or territory is not intended to be its own account. An account is the appropriate home for a *measure*, such as sales, units sold, or number of employees.
  

