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
(struct sum (arg)                #:transparent)
;(struct dot (arg1 arg2)          #:transparent)
(struct element* (arg1 arg2)     #:transparent)
(struct element+ (arg1 arg2)     #:transparent)
;(struct extend (arg1 arg2)       #:transparent)
(struct matmul (arg1) (arg2)     #:transparent)
(struct slice-col (arg1) (arg2)  #:transparent)
(struct eye-like (arg)           #:transparent)
(struct eye-like-squares (arg)   #:transparent)
(struct zeros-like (arg)         #:transparent)
(struct ones-like (arg)          #:transparent)



; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.

(define (index a i j) (list-ref (list-ref a i) j))
(define (elementwise a b op) (let a_ = (interpret a), b_ = (interpret b) in
                             (if 
                               (and (equals? (length a_) (length b_)) (equals? (length (car a_)) (length (car b_))))
                               (build-list (length a_)  (lambda (i) (build-list (length (car a_)) (lambda (j) (op (index a_ i j) (index b_ i j)  ))))) 
                               (assert #f) )))

; TODO use lists instead of arrays?
(define (interpret p)
  (match p
    [(transpose a)         (array-axis-swap (interpret a) 0 1)]
    [(sum a)               (list (list (apply + (interpret a))))]
    [(element* a b)        (elementwise a b *)]
    [(element+ a b)        (elementwise a b +)]
    ;[(dot a b)             (sum (element* (interpret a) (interpret b)))]
    ;[(extend a b)          (array-list->array (list (interpret a) (interpret b)))]
    [(eye-like a)          (build-list (length a) (lambda (id) (build-list (length (car a)) (lambda (id2) (if (equals? id id2) 1 0)))))]
    [(eye-like-squares a)  (build-list (length a) (lambda (id) (build-list (length a)       (lambda (id2) (if (equals? id id2) 1 0)))))]
    [(zeros-like a)        (build-list (length a) (lambda (id) (build-list (length (car a)) (lambda (id2) 0 ))))  ]
    [(ones-like a)         (build-list (length a) (lambda (id) (build-list (length (car a)) (lambda (id2) 1 ))))  ]
    [(matmul a b)          (let a_ = (interpret a), b_ = (transpose (interpret b)) in
                             (if 
                               (equals? (length (car a_)) (length b_))
                               (build-list (length a_) (lambda (i) (build-list (length b_) (lambda (j) (apply + (element* (list-ref a_ i) (list-ref b_ j)))))))
                               (assert #f) ))]
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
;           (dot a b)
;           (extend a b)
           (eye a)
           (eye-like a)
           (eye-like-squares a)
           (zeros-like a)
           (ones-like a)
           (matmul a b)
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
