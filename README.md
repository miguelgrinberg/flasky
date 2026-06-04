# Flasky — Tags REST API Enhancement

## Original Project
**Repository:** https://github.com/miguelgrinberg/flasky  
**Author:** Miguel Grinberg  
**Description:** A full-featured Flask blog application accompanying the book
*Flask Web Development* (O'Reilly). Created in 2014.

---

## My Enhancement: Tags CRUD API

**Branch:** `feature/tags-api`  
**Added by:** gailsanchez

### What & Why

Blog posts without tags are hard to discover. This enhancement adds a fully
RESTful **Tags** resource to Flasky's existing `/api/v1/` blueprint, letting
clients create, read, update, and delete tags and associate them with posts.

---

## API Endpoints

| Method | Endpoint                  | Auth? | Description                  | Status      |
|--------|---------------------------|-------|------------------------------|-------------|
| GET    | `/api/v1/tags/`           | No    | List all tags                | 200         |
| POST   | `/api/v1/tags/`           | Yes   | Create a new tag             | 201/400     |
| GET    | `/api/v1/tags/<id>`       | No    | Get a single tag             | 200/404     |
| PUT    | `/api/v1/tags/<id>`       | Yes   | Update a tag's name          | 200/400/404 |
| DELETE | `/api/v1/tags/<id>`       | Yes   | Delete a tag                 | 200/404     |
| GET    | `/api/v1/tags/<id>/posts` | No    | List posts carrying this tag | 200/404     |

**Authentication:** HTTP Basic Auth using email + password.

---

## Files Changed
