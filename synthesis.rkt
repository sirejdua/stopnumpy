#lang rosette/safe

(require rosette/lib/angelic  ; provides `choose*`
         rosette/lib/match    ; provides `match`
         math/array           ; matrix support
         (only-in python py-import py-method-call)
         ;python/config
         )
; Tell Rosette we really do want to use integers.
(current-bitwidth #f)

; Only needs to be done once
;(enable-cpyimport!)

; Import python module
(py-import "prog" as python-module)
(py-method-call python-module "destruct" 
  (py-method-call python-module "construct" (list (list 1 2) (list 3 4))))


; Syntax for DSL
(struct transpose (arg) #:transparent)


; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.
(define (interpret p)
  (match p
    [(transpose a)  (apply map list (interpret a))]
    [_ p]))


; Create an unknown expression -- one that can evaluate to several
; possible values.
(define (??expr terminals)
  (define a (apply choose* terminals))
  (choose* (transpose a)
           a))

(define-symbolic* a11 integer?)
(define-symbolic* a12 integer?)
(define-symbolic* a21 integer?)
(define-symbolic* a22 integer?)

; Variables 
(define x 
  (list (list a11 a12) (list a21 a22)))


(define sketch
  (??expr (list x)))

(define (prog x)
  (py-method-call python-module "transpose" x))

(define M
  (synthesize
    #:forall (list x)
    #:guarantee (assert (equal? (interpret sketch) prog))))

M

; Substitute the bindings in M into the sketch to get back the
; synthesized program.
(evaluate sketch M)