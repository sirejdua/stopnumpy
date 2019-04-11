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

(define y1 (array #[#[1 2]#[3 4]]))

; Import python module
(py-import "prog" as python-module)
(py-method-call python-module "transpose_py" y1)

; Syntax for DSL
(struct transpose (arg)        #:transparent)
(struct sum (arg)              #:transparent)
(struct dot (arg1 arg2)      #:transparent)
(struct element* (arg1 arg2) #:transparent)
(struct element+ (arg1 arg2) #:transparent)
(struct extend (arg1 arg2)   #:transparent)
(struct eye (arg)              #:transparent)



; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.
(define (interpret p)
  (match p
    [(transpose a)    (array-axis-swap (interpret a) 0 1)]
    [(sum a)          (apply + (array->list (interpret a)))]
    [(element* a b)   (map * (array->list (interpret a) (array->list (interpret b))))]
    [(element+ a b)   (map + (array->list (interpret a) (array->list (interpret b))))]
    [(dot a b)        (sum (element* (interpret a) (interpret b)))]
    [(extend a b)     (array-list->array (list (interpret a) (interpret b)))]
    [(eye n)          (build-array #(n n) (lambda (ids) (if (equal? (vector-ref ids 0) (vector-ref ids 1)) 1 0 )))  ]
    [_ p]))


; Create an unknown expression -- one that can evaluate to several
; possible values.
(define (??expr terminals)
  (define a (apply choose* terminals))
  (define b (apply choose* terminals))
  (choose* (transpose a)
           (sum a)
           (element* a b)
           (element+ a b)
           (dot a b)
           (extend a b)
           ;(eye a)
           a))


(define (make-int x)
  (define-symbolic* i integer?)
  i)
(define (make-array n) 
  (build-array #(3 3) make-int))

; Variables 
(define x (make-array 2))
;(define y (make-array 2))
;(define z (make-array 2))
;(define a (make-int a))
;(define b (make-int b))
;(define c (make-int c))


(define sketch
  (??expr (list x)))

(define prog
  (py-method-call python-module "transpose_py" x))

(define M
  (synthesize
    #:forall (list x)
    #:guarantee (assert (equal? (interpret sketch) prog))))

M

; Substitute the bindings in M into the sketch to get back the
; synthesized program.
(evaluate sketch M)
